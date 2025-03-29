# Use the official Nginx image
FROM nginx:latest

# Remove default Nginx config and replace with our custom config
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx-custom.conf /etc/nginx/conf.d/default.conf

# Copy Angular build files (Make sure you have built your Angular app)
COPY dist/browser/ /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]