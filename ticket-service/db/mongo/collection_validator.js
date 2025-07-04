db.createCollection("theaters", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: ["theater_id", "cinema_id", "name", "capacity", "theater_type", "seats", "is_active"],
         properties: {
            theater_id: {
               bsonType: "int",
               description: "must be an integer and is required"
            },
            cinema_id: {
               bsonType: "int",
               description: "must be an integer and is required"
            },
            name: {
               bsonType: "string",
               description: "must be a string and is required",
               minLength: 3,
               maxLength: 100
            },
            capacity: {
               bsonType: "int",
               description: "must be an integer and is required",
               minimum: 1
            },
            theater_type: {
               bsonType: "string",
               enum: ["STANDARD", "VIP", "IMAX", "PREMIUM", "DOLBY_ATMOS"],
               description: "must be one of the allowed enum values and is required"
            },
            seats: {
               bsonType: "array",
               description: "must be an array of seat objects and is required",
               items: {
                  bsonType: "object",
                  required: ["seat_id", "theater_id", "seat_row", "seat_number", "seat_type"],
                  properties: {
                     seat_id: { bsonType: "int" },
                     theater_id: { bsonType: "int" },
                     seat_row: { bsonType: "string", minLength: 1, maxLength: 2 },
                     seat_number: { bsonType: "int", minimum: 1 },
                     seat_type: { bsonType: "string", enum: ["STANDARD", "VIP", "ACCESSIBLE", "PREMIUM"] },
                     is_active: { bsonType: "bool" },
                     created_at: { bsonType: "date" },
                     updated_at: { bsonType: "date" }
                  }
               }
            },
            is_active: {
               bsonType: "bool",
               description: "must be a boolean and is required"
            },
            maintenance_mode: {
               bsonType: "bool",
               description: "must be a boolean"
            },
            created_at: {
               bsonType: "date",
               description: "must be a date"
            },
            updated_at: {
               bsonType: "date",
               description: "must be a date"
            }
         }
      }
   },
   validationAction: "error"
})


db.theaters.insertOne(
   {
      "theater_id": 101,
      "cinema_id": 1,
      "name": "Sala Principal",
      "capacity": 150,
      "theater_type": "STANDARD",
      "seats": [
         {
            "theater_id": 101,
            "seat_row": "A",
            "seat_number": 1,
            "seat_type": "STANDARD",
            "is_active": true,
            "created_at": "2025-07-02T14:00:00.000Z",
            "updated_at": "2025-07-02T14:00:00.000Z"
         },
         {
            "theater_id": 101,
            "seat_row": "A",
            "seat_number": 2,
            "seat_type": "STANDARD",
            "is_active": true,
            "created_at": "2025-07-02T14:00:00.000Z",
            "updated_at": "2025-07-02T14:00:00.000Z"
         },
         {
            "theater_id": 101,
            "seat_row": "B",
            "seat_number": 1,
            "seat_type": "VIP",
            "is_active": true,
            "created_at": "2025-07-02T14:00:00.000Z",
            "updated_at": "2025-07-02T14:00:00.000Z"
         }
      ],
      "is_active": true,
      "maintenance_mode": false,
      "created_at": "2025-07-02T14:00:00.000Z",
      "updated_at": "2025-07-02T14:00:00.000Z"
   }
)