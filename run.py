from flask import Flask
import os
from app import app

if __name__ == "__main__":
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(host="0.0.0.0",debug=True)