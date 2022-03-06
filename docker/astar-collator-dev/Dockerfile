FROM ubuntu:20.04

LABEL maintainer="polonity <hiken.pc@gmail.com>"

RUN apt update
RUN apt install -y \
wget

RUN wget -O - https://github.com/AstarNetwork/Astar/releases/download/v3.10.0/astar-collator-3.10.0-ubuntu-x86_64.tar.gz | tar xzf - 

CMD ["./astar-collator", "--tmp", "--port", "30333" ,"--ws-port", "9944", "--rpc-port", "9933", "--rpc-cors", "all", "--alice", "--dev", "--unsafe-ws-external",  "--unsafe-rpc-external"]
