FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /usr/share/nginx/html/index.html
COPY diary.html /usr/share/nginx/html/diary.html
COPY view-diary.html /usr/share/nginx/html/view-diary.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
