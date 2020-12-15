package com.asts.server.controller;

import com.asts.server.dto.JSONResult;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController("/")
public class StockController {

    @GetMapping
    public ResponseEntity getTest() {
        return ResponseEntity.status(HttpStatus.OK).body(JSONResult.success(null,"test"));
    }
}
