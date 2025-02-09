import { createServer } from "http";
import { Server as SocketIoServer } from "socket.io";
import { io as SocketIoClient } from "socket.io-client";
import next from "next";

const dev = process.env.NODE_ENV !== "production";
const app = next({ dev });
const handle = app.getRequestHandler();
const PORT = process.env.PORT || 3000;
const BASE_URL = process.env.BASE_URL || `http://localhost:${PORT}`;

app.prepare().then(() => {
  const server = createServer((req, res) => handle(req, res));
  const ioServer = new SocketIoServer(server, {
    cors: {
      origin: BASE_URL,
    },
    path: "/socket.io",
  });

  const DISCORD_BOT_URL = process.env.DISCORD_BOT_URL;
  if (!DISCORD_BOT_URL) {
    throw new Error("DISCORD_BOT_URL is not defined!");
  }
  const discordBotSocket = SocketIoClient(DISCORD_BOT_URL);

  ioServer.on("connection", (clientSocket) => {
    discordBotSocket.on("update", (data) => {
      clientSocket.emit("update", data);
    });
  });

  server.listen(PORT, () => {
    console.log(`Next.js + Socket.io server running ON ${BASE_URL}`);
  });
});