// server.ts
import { createServer } from "http";
import { Server as SocketIoServer } from "socket.io";
import { io as SocketIoClient } from "socket.io-client";
import next from "next";

const dev = process.env.NODE_ENV !== "production";
const app = next({ dev });
const handle = app.getRequestHandler();
const PORT = process.env.PORT || 3000;

const BASE_URL = process.env.BASE_URL || `http://localhost:${PORT}`;

// Initialize Next.js and Socket.io
app.prepare().then(() => {
  const server = createServer((req, res) => handle(req, res));
  const ioServer = new SocketIoServer(server, {
    cors: {
      origin: BASE_URL,
    },
    path: "/socket.io",
  });

  // Connect to Discord Bot
  const DISCORD_BOT_URL = process.env.DISCORD_BOT_URL;
  if (!DISCORD_BOT_URL) {
    throw new Error("DISCORD_BOT_URL is not defined!");
  }
  const discordBotSocket = SocketIoClient(DISCORD_BOT_URL);

  // Relay messages between client and Discord bot
  ioServer.on("connection", (clientSocket) => {
    clientSocket.on("update", (data) => {
      discordBotSocket.emit("update", data);
    });

    discordBotSocket.on("update", (data) => {
      clientSocket.emit("update", data);
    });
  });

  // Start the server
  server.listen(PORT, () => {
    console.log(`Next.js + Socket.io server running on port ${PORT}`);
  });
});