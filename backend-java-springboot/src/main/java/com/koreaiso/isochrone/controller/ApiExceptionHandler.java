package com.koreaiso.isochrone.controller;

import com.koreaiso.isochrone.exception.OtpClientException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class ApiExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(ApiExceptionHandler.class);

    @ExceptionHandler(OtpClientException.class)
    public ResponseEntity<Map<String, Object>> handleOtpClientException(OtpClientException ex) {
        log.warn("OTP client error: {}", ex.getMessage());
        Map<String, Object> body = new HashMap<>();
        body.put("error", "OTP_REQUEST_FAILED");
        body.put("message", ex.getMessage());
        body.put("otpStatus", ex.getStatusCode());
        return ResponseEntity.status(HttpStatus.BAD_GATEWAY).body(body);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleGenericException(Exception ex) {
        log.error("Unexpected error", ex);
        Map<String, Object> body = new HashMap<>();
        body.put("error", "UNEXPECTED_ERROR");
        body.put("message", ex.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(body);
    }
}
