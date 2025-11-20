package com.koreaiso.isochrone.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "otp.api")
public class OtpClientProperties {

    /**
     * Base URL of the OTP service, e.g. http://otp:8080/otp
     */
    private String baseUrl = "http://otp:8080/otp";

    public String getBaseUrl() {
        return baseUrl;
    }

    public void setBaseUrl(String baseUrl) {
        this.baseUrl = baseUrl;
    }
}
