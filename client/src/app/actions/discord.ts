"use server";

const DISCORD_BOT_URL = process.env.DISCORD_BOT_URL;
if (!DISCORD_BOT_URL) {
  throw new Error("Can't connect to Discord Bot");
}

export const getDiscordData = async () => {
  try {
    const response = await fetch(`${DISCORD_BOT_URL}/api/users`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to get Discord data");
  }
};

export const dmDiscordUser = async (userId: string, formData: FormData, method = "POST") => {
  try {
    const message = formData.get("message");
    await fetch(`${DISCORD_BOT_URL}/api/users/dm/${userId}`, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
      }),
    });
  } catch (error) {
    console.error(error);
    throw new Error("Failed to warn Discord user");
  }
};
