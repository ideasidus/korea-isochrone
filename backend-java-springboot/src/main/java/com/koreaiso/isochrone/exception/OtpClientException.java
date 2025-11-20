package com.koreaiso.isochrone.exception;

public class OtpClientException extends RuntimeException {

    private final int statusCode;

    public OtpClientException(String message, int statusCode) {
        super(message);
        this.statusCode = statusCode;
    }

    public int getStatusCode() {
        return statusCode;
    }
}
