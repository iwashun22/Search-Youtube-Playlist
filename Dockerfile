FROM rust:1-alpine3.22

ARG TARGET
RUN rustup target add $TARGET

WORKDIR /app

