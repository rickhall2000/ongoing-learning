from golang:latest
WORKDIR /myapp
COPY welcome.go .
# Go expects modules now
RUN go mod init hello
RUN go build -o welcome .
ENTRYPOINT ["./welcome"]
