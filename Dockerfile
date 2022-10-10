FROM ubuntu:22.04

WORKDIR /app

COPY . .

# install packages
RUN sh setup/install_packages.sh

CMD ["sh", "run.sh"]