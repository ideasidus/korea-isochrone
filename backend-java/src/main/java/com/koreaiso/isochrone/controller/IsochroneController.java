package com.koreaiso.isochrone.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.koreaiso.isochrone.dto.IsochroneRequest;
import com.koreaiso.isochrone.service.IsochroneService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/isochrone")
@Validated
public class IsochroneController {

    private final IsochroneService isochroneService;

    public IsochroneController(IsochroneService isochroneService) {
        this.isochroneService = isochroneService;
    }

    @GetMapping
    public ResponseEntity<JsonNode> getIsochrone(@Valid IsochroneRequest request) {
        JsonNode response = isochroneService.fetchIsochrone(request);
        return ResponseEntity.ok(response);
    }
}
