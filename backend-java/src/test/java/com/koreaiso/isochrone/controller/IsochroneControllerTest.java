package com.koreaiso.isochrone.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.koreaiso.isochrone.service.IsochroneService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(controllers = IsochroneController.class)
class IsochroneControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private IsochroneService isochroneService;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Test
    void getIsochroneReturnsResponse() throws Exception {
        JsonNode jsonNode = objectMapper.readTree("{""type"":""FeatureCollection""}");
        Mockito.when(isochroneService.fetchIsochrone(any())).thenReturn(jsonNode);

        mockMvc.perform(get("/api/isochrone")
                        .param("fromPlace", "37.5665,126.9780")
                        .param("cutoffSec", "1800"))
                .andExpect(status().isOk())
                .andExpect(content().json("{""type"":""FeatureCollection""}"));
    }
}
