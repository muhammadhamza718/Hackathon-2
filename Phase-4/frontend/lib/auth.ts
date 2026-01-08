import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Create a database connection pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false,
  },
});

export const auth = betterAuth({
  database: pool,
  emailAndPassword: {
    enabled: true,
  },
  secret:
    process.env.BETTER_AUTH_SECRET || "fallback-secret-key-for-development",
  jwt: {
    expiresIn: "7d", // 7 days
  },
  session: {
    expires: "7d", // 7 days
    cookieCache: {
      enabled: true,
      maxAge: 7 * 24 * 60 * 60, // 7 days in seconds
    },
  },
  user: {
    additionalFields: {
      role: {
        type: "string",
        defaultValue: "user",
        required: false,
      },
    },
  },
});
