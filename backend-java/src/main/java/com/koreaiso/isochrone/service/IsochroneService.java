package com.koreaiso.isochrone.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.koreaiso.isochrone.client.OtpClient;
import com.koreaiso.isochrone.dto.IsochroneRequest;
import org.springframework.stereotype.Service;

@Service
public class IsochroneService {

    private final OtpClient otpClient;

    public IsochroneService(OtpClient otpClient) {
        this.otpClient = otpClient;
    }

    public JsonNode fetchIsochrone(IsochroneRequest request) {
        return otpClient.fetchIsochrone(request.toQueryParams());
    }
}
