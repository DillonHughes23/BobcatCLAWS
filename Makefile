DB_DUMP_FILE = database_dump.sql
DB_NAME = "BobcatClawsDB"
DB_USERNAME = "BobcatClawsDev"
DB_PASSWORD = "CS#4398DB"
DB_CREDENTIALS_FILE = db_credentials.cnf
APP_NAME = "webapp"
PROJECT_DIR = "Software-Engineering-Project-Course"
NGINX_CONFIG = "nginx_config"

NODE_VERSION = v21.1.0
NODE_DIST = node-$(NODE_VERSION)-linux-x64
NODE_PREFIX = /usr/local # or another directory where you have write permission

# Targets and their corresponding commands
.PHONY:
	all install-dependencies build-angular-test build-angular-production start setup-db load-dump configure-nginx clean

all:
	$(MAKE) install-dependencies
	$(MAKE) setup-db
	$(MAKE) build-angular-test
	#$(MAKE) configure-nginx
	#$(MAKE) start

install-dependencies:
	# Download the specified Node.js version tarball
	@echo "Downloading Node.js $(NODE_VERSION)..."
	@curl -o /tmp/$(NODE_DIST).tar.xz https://nodejs.org/dist/$(NODE_VERSION)/$(NODE_DIST).tar.xz

    	# Extract the tarball
	@echo "Extracting Node.js $(NODE_VERSION)..."
	@tar -C /tmp -xf /tmp/$(NODE_DIST).tar.xz

    	# Install Node.js binaries
	@echo "Installing Node.js $(NODE_VERSION)..."
	@sudo cp -R /tmp/$(NODE_DIST)/bin $(NODE_PREFIX)
	@sudo cp -R /tmp/$(NODE_DIST)/include $(NODE_PREFIX)
	@sudo cp -R /tmp/$(NODE_DIST)/lib $(NODE_PREFIX)
	@sudo cp -R /tmp/$(NODE_DIST)/share $(NODE_PREFIX)
	# Update system links for node and npm
	#@sudo ln -sf $(NODE_PREFIX)/bin/node /usr/local/bin/node
	#@sudo ln -sf $(NODE_PREFIX)/bin/npm /usr/local/bin/npm
	#@sudo ln -sf $(NODE_PREFIX)/bin/npx /usr/local/bin/npx
	
	#@export PATH=$(NODE_PREFIX)/bin:$PATH
	# Clean up downloaded file
	@rm /tmp/$(NODE_DIST).tar.xz
	# Install Angular CLI
	@echo "Installing Angular CLI..."
	sudo npm install -g @angular/cli
	
	sudo apt install -y python3-pip
	# Assuming there's a requirements.txt in the project directory for pip dependencies
	if [ -f "requirements.txt" ]; then \
	sudo pip3 install -r requirements.txt; \
	fi
	# Install pm2
	sudo npm install -g pm2
	sudo npm install dotenv

setup-db: create-db-credentials
	# Create MySQL database
	echo "CREATE DATABASE IF NOT EXISTS $(DB_NAME);" | sudo mysql -u $(DB_USERNAME) -p$(DB_PASSWORD)
	# Load dump file into MySQL database
	if [ -f "$(DB_DUMP_FILE)" ]; then \
		sudo mysql -u $(DB_USERNAME) -p$(DB_PASSWORD) $(DB_NAME) < $(DB_DUMP_FILE); \
	fi

create-db-credentials:
	@echo "[client]" > $(DB_CREDENTIALS_FILE)
	@echo "db_name=$(DB_NAME)" >> $(DB_CREDENTIALS_FILE)
	@echo "user=$(DB_USERNAME)" >> $(DB_CREDENTIALS_FILE)
	@echo "password=$(DB_PASSWORD)" >> $(DB_CREDENTIALS_FILE)
	@echo "Database credentials written to $(DB_CREDENTIALS_FILE)"

build-angular-production:
	# Navigate to the Angular project directory and build the project
	cd src/ && ng build --configuration=production
build-angular-test:
	cd src/ && ng serve --port 8080

configure-nginx:
	# Copy the nginx config file to the sites-available directory
	sudo cp $(NGINX_CONFIG) /etc/nginx/sites-available/$(APP_NAME)
	# Remove any existing symbolic link to ensure no conflict
	sudo rm -f /etc/nginx/sites-enabled/$(APP_NAME)
	# Create a symbolic link in the sites-enabled directory
	sudo ln -s /etc/nginx/sites-available/$(APP_NAME) /etc/nginx/sites-enabled/	
	# Test the NGINX configuration
	sudo nginx -t
	# Reload NGINX to apply the new configuration
	sudo systemctl reload nginx

start:
	# Start serving the app with pm2
	pm2 start dist/$(APP_NAME) --name $(APP_NAME)

clean:
	# Clean the build files and other artifacts
	rm -rf dist/

# Add any additional targets you might need
