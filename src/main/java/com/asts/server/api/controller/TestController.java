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
public class TestController {       //테스트

    private final MovieRepository movieRepository;

    @GetMapping
    public ResponseEntity getTest() {
        Movie movie = new Movie();
        movie.setTitle("Title");
        movie.setImdbId("imdbID");
        movie.setPoster("Poster");
        movie.setYear(123);
        movie.setType("Type");
        Movie result = movieRepository.save(movie);
        if(result!=null) {
            System.out.println(result.getId()+"아이디 값, 제대로 찍힘");
        }
        return ResponseEntity.status(HttpStatus.OK).body(JSONResult.success(null,"test"));
    }
}
