FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
# Leggi la variabile d'ambiente DOMAIN dal file .env e sostituisci nel file di configurazione Nginx
RUN sed -i "s/\$DOMAIN/$(grep DOMAIN ../config/.env | cut -d '=' -f2)/" /etc/nginx/conf.d/nginx.conf

