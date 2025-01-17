import { NextResponse } from "next/server";
import { getUsers } from "../../lib/data";

export const GET = async () => {
  try {
    const users = await getUsers();
    return new NextResponse(JSON.stringify(users), { status: 200 });
  } catch (error) {
    console.error(error);
    return new NextResponse("Failed to get users", { status: 500 });
  }
};
