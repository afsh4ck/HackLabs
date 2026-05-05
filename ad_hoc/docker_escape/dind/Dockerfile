FROM docker:27-dind

# Herramientas necesarias para técnicas de resolución dentro del host aislado
RUN apk add --no-cache bash curl python3

# Flag real del lab dentro del host simulado del escenario aislado (dind)
RUN mkdir -p /root && echo 'HL{c0n741n3r_35c4p3_h057_4cc355}' > /root/root.txt
