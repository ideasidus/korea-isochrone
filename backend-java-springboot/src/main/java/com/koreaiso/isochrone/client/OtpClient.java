package com.koreaiso.isochrone.client;

import com.fasterxml.jackson.databind.JsonNode;
import com.koreaiso.isochrone.exception.OtpClientException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Component;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class OtpClient {

    private static final Logger log = LoggerFactory.getLogger(OtpClient.class);

    private final WebClient webClient;

    public OtpClient(WebClient webClient) {
        this.webClient = webClient;
    }

    public JsonNode fetchIsochrone(MultiValueMap<String, String> params) {
        return webClient.get()
                .uri(uriBuilder -> {
                    uriBuilder.path("/routers/default/isochrone");
                    params.forEach((key, values) -> values.forEach(value -> uriBuilder.queryParam(key, value)));
                    return uriBuilder.build();
                })
                .retrieve()
                .onStatus(HttpStatusCode::isError, this::handleError)
                .bodyToMono(JsonNode.class)
                .block();
    }

    private Mono<? extends Throwable> handleError(ClientResponse response) {
        return response.bodyToMono(String.class)
                .defaultIfEmpty("OTP error without body")
                .flatMap(body -> {
                    int status = response.statusCode().value();
                    log.error("OTP API error status={} body={} ", status, body);
                    return Mono.error(new OtpClientException(body, status));
                });
    }
}
