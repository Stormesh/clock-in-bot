import { NextResponse } from "next/server";
import { getRoles } from "../../lib/data";

export const GET = async () => {
  try {
    const roles = await getRoles();
    return new NextResponse(JSON.stringify(roles), { status: 200 });
  } catch (error) {
    console.error(error);
    return new NextResponse("Failed to get roles", { status: 500 });
  }
};
