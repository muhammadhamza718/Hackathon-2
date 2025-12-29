const { Pool } = require("pg");
const fs = require("fs");
const path = require("path");

// Basic dotenv parser to avoid dependency if not installed
function parseEnv(filePath) {
  if (!fs.existsSync(filePath)) return {};
  const content = fs.readFileSync(filePath, "utf8");
  const env = {};
  content.split("\n").forEach((line) => {
    const match = line.match(/^([^=]+)=(.*)$/);
    if (match) {
      const key = match[1].trim();
      let value = match[2].trim();
      // Remove quotes if present
      if (value.startsWith('"') && value.endsWith('"'))
        value = value.slice(1, -1);
      if (value.startsWith("'") && value.endsWith("'"))
        value = value.slice(1, -1);
      env[key] = value;
    }
  });
  return env;
}

// Load envs
const envLocal = parseEnv(path.join(__dirname, ".env.local"));
const env = parseEnv(path.join(__dirname, ".env"));
const mergedEnv = { ...env, ...envLocal };

const connectionString = mergedEnv.DATABASE_URL || process.env.DATABASE_URL;

console.log("--- Database Connection Diagnostic ---");
console.log("Checking connection string...");

if (!connectionString) {
  console.error("❌ ERROR: DATABASE_URL is missing in .env or .env.local");
  process.exit(1);
}

// Mask password for display
const maskedUrl = connectionString.replace(/:([^:@]+)@/, ":****@");
console.log(`URL found: ${maskedUrl}`);

if (connectionString.includes("+asyncpg")) {
  console.error(
    '❌ ERROR: Connection string uses "asyncpg" scheme (Python specific). Frontend needs standard "postgresql://".'
  );
  console.log(
    '👉 Fix: Change "postgresql+asyncpg://" to "postgresql://" in your frontend .env file.'
  );
  process.exit(1);
}

const pool = new Pool({
  connectionString: connectionString,
});

pool.connect((err, client, release) => {
  if (err) {
    console.error("❌ Connection Failed:", err.message);
    if (err.message.includes("password")) {
      console.error("👉 Hint: Check your database password in .env");
    }
    process.exit(1);
  }
  console.log("✅ Connection Successful!");

  client.query("SELECT NOW()", (err, result) => {
    release();
    if (err) {
      console.error("❌ Query Failed:", err.message);
      process.exit(1);
    }
    console.log("✅ Database responded:", result.rows[0]);
    console.log('Checking "user" table...');

    client.query(`SELECT to_regclass('public.user')`, (err, result) => {
      if (err) {
        console.error("❌ Check table failed:", err);
        process.exit(1);
      }
      if (result.rows[0].to_regclass) {
        console.log('✅ "user" table exists.');
      } else {
        console.error('❌ ERROR: "user" table DOES NOT EXIST. Run migrations!');
      }
      process.exit(0);
    });
  });
});
