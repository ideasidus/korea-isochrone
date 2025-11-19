package com.koreaiso.isochrone.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI isochroneOpenAPI() {
        return new OpenAPI()
                .components(new Components())
                .info(new Info()
                        .title("Korea Isochrone API")
                        .description("Spring Boot 래퍼를 통해 OTP Isochrone 엔드포인트를 호출하는 백엔드 API")
                        .version("v1")
                        .contact(new Contact().name("Korea Isochrone")));
    }
}
