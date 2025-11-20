package com.koreaiso.isochrone.config;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
@EnableConfigurationProperties(OtpClientProperties.class)
public class WebClientConfig {

    @Bean
    public WebClient otpWebClient(WebClient.Builder builder, OtpClientProperties properties) {
        return builder
                .baseUrl(properties.getBaseUrl())
                .build();
    }
}
