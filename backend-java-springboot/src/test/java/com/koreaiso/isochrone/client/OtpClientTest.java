package com.koreaiso.isochrone.client;

import com.fasterxml.jackson.databind.JsonNode;
import com.koreaiso.isochrone.config.OtpClientProperties;
import com.koreaiso.isochrone.exception.OtpClientException;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.client.WebClient;

import java.io.IOException;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class OtpClientTest {

    private MockWebServer mockWebServer;
    private OtpClient otpClient;

    @BeforeEach
    void setUp() throws IOException {
        mockWebServer = new MockWebServer();
        mockWebServer.start();

        OtpClientProperties props = new OtpClientProperties();
        props.setBaseUrl(mockWebServer.url("/otp").toString().replaceAll("/$", ""));

        WebClient webClient = WebClient.builder().baseUrl(props.getBaseUrl()).build();
        otpClient = new OtpClient(webClient);
    }

    @AfterEach
    void tearDown() throws IOException {
        mockWebServer.shutdown();
    }

    @Test
    void fetchIsochroneReturnsJson() {
        mockWebServer.enqueue(new MockResponse()
                .setResponseCode(200)
                .addHeader("Content-Type", "application/json")
                .setBody("{""type"":""FeatureCollection""}"));

        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
        params.add("fromPlace", "37.5665,126.9780");
        params.add("cutoffSec", "1800");

        JsonNode response = otpClient.fetchIsochrone(params);
        assertThat(response.get("type").asText()).isEqualTo("FeatureCollection");
    }

    @Test
    void fetchIsochroneThrowsOnError() {
        mockWebServer.enqueue(new MockResponse()
                .setResponseCode(500)
                .setBody("Internal error"));

        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
        params.add("fromPlace", "37.5665,126.9780");
        params.add("cutoffSec", "1800");

        assertThatThrownBy(() -> otpClient.fetchIsochrone(params))
                .isInstanceOf(OtpClientException.class)
                .hasMessageContaining("Internal error");
    }
}
