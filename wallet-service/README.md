# Cinema Wallet Service

## Overview

The Cinema Wallet Service is a microservice designed to manage the wallet accounts for cinema customers. It allows users to purchase items, receive promotions, and manage their wallet balance efficiently.

## Endpoints

- **GET /ping**: Returns a simple "pong" message to check the service status.
- **GET /health**: Provides the health status of the service.

## Architecture

The service is built using FastAPI and follows a clean architecture approach. The main components include:

- **PostgreSQL as the Database**: Used to store wallet information and transaction history.
- **RabbitMQ for Messaging**: Facilitates communication with other services, allowing events to be published and consumed asynchronously.

### Diagram

```plaintext
+---------------------------+
|   Cinema Wallet Service   |
|                           |
|  +---------------------+  |
|  |   FastAPI (API)     |  |
|  +---------------------+  |
|           |              |
|           v              |
|  +---------------------+  |
|  |   Business Logic    |  |
|  +---------------------+  |
|           |              |
|           v              |
|  +---------------------+  |
|  |      Database       |  |
|  |   (PostgreSQL)      |  |
|  +---------------------+  |
|           |              |
|           v              |
|  +---------------------+  |
|  |      Messaging      |  |
|  |     (RabbitMQ)      |  |
|  +---------------------+  |
+---------------------------+
```

## Features

- **Wallet Management**: Manage users' wallet balance, transactions, and history.
- **Promotions and Offers**: Handle promotions and allow users to avail special offers.
- **Event-driven Communication**: Utilize RabbitMQ to communicate with other microservices, such as order processing and notifications.

## Getting Started

To run the service, use:

```bash
uvicorn main:app --reload
```

Ensure all dependencies are installed via:

```bash
pip install -r requirements.txt
```
