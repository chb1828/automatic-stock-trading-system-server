package com.asts.server.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;


@Getter
@Setter
@ToString
@AllArgsConstructor
public class JSONResult {

    private String result;
    private String message;
    private Object data;

    public static JSONResult success(Object data) {
        return new JSONResult("success",null,data);
    }

    public static JSONResult success(Object data,String message) {
        return new JSONResult("success",message,data);
    }
    public static JSONResult fail(String message) {
        return new JSONResult("fail",message,null);
    }
}
