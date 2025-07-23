import dotenv from "dotenv";
import readline from "node:readline";
import { Permissions } from "./src/app/lib/enums";
import {
  createRoles,
  createUser,
  getRoleByName,
  getUsers,
} from "./src/app/lib/data";
import { Types } from "mongoose";
import { hash } from "bcryptjs";

let env = "./.env.local";

if (process.env.NODE_ENV === "production") env = "./.env.production.local";

dotenv.config({ path: `./${env}` });

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const roles = [
  {
    name: "superadmin",
    priority: 0,
    permissions: [
      Permissions.SignUp,
      Permissions.Delete,
      Permissions.Update,
      Permissions.Kick,
      Permissions.Warn,
      Permissions.Logs,
    ],
  },
  {
    name: "admin",
    priority: 1,
    permissions: [
      Permissions.SignUp,
      Permissions.Kick,
      Permissions.Warn,
      Permissions.Logs,
    ],
  },
  {
    name: "user",
    priority: 2,
    permissions: [Permissions.Kick, Permissions.Warn],
  },
  {
    name: "client",
    priority: 3,
  },
];

const isEmpty = (str: string) => {
  return str.trim() === "" || str.trim().length === 0;
};

(async () => {
  const users = await getUsers();
  if (users.length > 0) {
    console.error("Database is already initialized");
    process.exit(1);
  }

  rl.question(
    "\x1b[33mEnter the username for the root account: \x1b[0m",
    (name) => {
      if (isEmpty(name)) {
        console.error("Username is required");
        process.exit(1);
      }

      rl.question(
        "\x1b[33mEnter the password for the root account: \x1b[0m",
        async (password) => {
          if (isEmpty(password)) {
            console.error("Password is required");
            process.exit(1);
          }

          if (password.length < 8) {
            console.error("Password must be at least 8 characters");
            process.exit(1);
          }

          const hashedPassword = await hash(password, 10);

          try {
            await createRoles(roles);
            console.log("\x1b[32mRoles created successfully.\x1b[0m");
            try {
              const rootRole = await getRoleByName("superadmin");
              await createUser(
                name,
                hashedPassword,
                rootRole._id as Types.ObjectId
              );
              console.log("\x1b[32mRoot user created successfully.\x1b[0m");
            } catch (error) {
              console.error("Error creating root user:", error);
              process.exit(1);
            }
          } catch (error) {
            console.error("Error creating roles:", error);
            process.exit(1);
          } finally {
            rl.close();
            process.exit(0);
          }
        }
      );
    }
  );
})();
