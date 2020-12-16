package com.asts.server.api.controller;

import com.asts.server.core.domain.Movie;
import com.asts.server.core.repository.MovieRepository;
import com.asts.server.dto.JSONResult;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RequiredArgsConstructor
@RestController("/")
public class TestController {
    //주석처리

    private final MovieRepository movieRepository;

    @GetMapping
    public ResponseEntity getTest() {
        Movie movie = new Movie();
        movie.setTitle("Title");
        movie.setImdbId("imdbID");
        movie.setPoster("Poster");
        movie.setYear(123);
        movie.setType("Type");
        movieRepository.save(movie);
        return ResponseEntity.status(HttpStatus.OK).body(JSONResult.success(null,"test"));
    }
}
