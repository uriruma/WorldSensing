# MYSQL server
FROM mysql:8.0.27

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=python_test
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=root

# Copy custom configuration file to container
COPY my.cnf /etc/mysql/conf.d/

# Expose port 3306 for outside communication
EXPOSE 3306