package com.asts.server.core.domain;

import com.asts.server.core.domain.audit.DateAudit;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Movie extends DateAudit {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String title;
    private Integer year;
    private String imdbId;
    private String type;
    private String poster;
}
