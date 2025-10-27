# DocuSign Button Application

A simple web application with a "Start with DocuSign" button that redirects to a DocuSign webform URL over HTTPS.

## Files

- `index.html` - Main web page with the DocuSign button
- `simple_https_server.py` - HTTPS server to serve the application
- `cert.pem` & `key.pem` - SSL certificates (auto-generated)

## Prerequisites

- Python 3.x
- OpenSSL (for SSL certificate generation)

## Setup & Installation

1. **Clone or download** this project to your local machine

2. **Navigate to the project directory:**
   ```bash
   cd /path/to/DSButton
   ```

3. **Ensure Python 3 is installed:**
   ```bash
   python3 --version
   ```

## Running the Application

### Method 1: Using the Python HTTPS Server (Recommended)

1. **Start the HTTPS server:**
   ```bash
   python3 simple_https_server.py
   ```

2. **SSL certificates will be automatically created** if they don't exist

3. **Access the application:**
   - Open your browser and go to: `https://localhost:8443`
   - You may see a security warning about the self-signed certificate - click "Advanced" and "Proceed to localhost"

4. **Stop the server:**
   - Press `Ctrl+C` in the terminal

### Method 2: Using Python's Built-in HTTP Server (Alternative)

If you don't need HTTPS, you can use a simple HTTP server:

```bash
python3 -m http.server 8080
```

Then access: `http://localhost:8080`

## Usage

1. Open the application in your web browser
2. Click the "Start with DocuSign" button
3. The page will redirect to the configured DocuSign webform URL

## Configuration

To change the DocuSign URL:

1. Open `index.html`
2. Find the `docuSignUrl` variable in the JavaScript section
3. Replace the URL with your desired DocuSign webform URL
4. Save the file and refresh the browser

## Troubleshooting

### SSL Certificate Issues
- If you encounter SSL certificate errors, the server will automatically generate new self-signed certificates
- For production use, replace the self-signed certificates with proper SSL certificates

### Port Already in Use
- If port 8443 is already in use, you can modify the `PORT` variable in `simple_https_server.py`
- Or kill the existing process using the port

### OpenSSL Not Found
- On Ubuntu/Debian: `sudo apt-get install openssl`
- On macOS: `brew install openssl`
- On Windows: Download OpenSSL from the official website

## Technical Details

- **Server**: Python 3 with built-in `http.server` and `ssl` modules
- **SSL**: Self-signed certificates for local development
- **Port**: 8443 (HTTPS) or 8080 (HTTP alternative)
- **Browser Compatibility**: Works with all modern browsers

## Security Note

This application uses self-signed SSL certificates for local development. For production deployment, use proper SSL certificates from a trusted Certificate Authority.