package com.koreaiso.isochrone.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

public class IsochroneRequest {

    @NotBlank
    private String fromPlace;

    @NotNull
    private Integer cutoffSec;

    private String mode;

    private String date;

    private String time;

    public String getFromPlace() {
        return fromPlace;
    }

    public void setFromPlace(String fromPlace) {
        this.fromPlace = fromPlace;
    }

    public Integer getCutoffSec() {
        return cutoffSec;
    }

    public void setCutoffSec(Integer cutoffSec) {
        this.cutoffSec = cutoffSec;
    }

    public String getMode() {
        return mode;
    }

    public void setMode(String mode) {
        this.mode = mode;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public MultiValueMap<String, String> toQueryParams() {
        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
        params.add("fromPlace", fromPlace);
        params.add("cutoffSec", String.valueOf(cutoffSec));
        if (mode != null && !mode.isBlank()) {
            params.add("mode", mode);
        }
        if (date != null && !date.isBlank()) {
            params.add("date", date);
        }
        if (time != null && !time.isBlank()) {
            params.add("time", time);
        }
        return params;
    }
}
