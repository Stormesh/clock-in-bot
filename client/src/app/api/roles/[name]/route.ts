import { getRoleByName } from "@/src/app/lib/data";
import { NextRequest, NextResponse } from "next/server";

export const GET = async (
  req: NextRequest,
  { params }: { params: Promise<{ name: string }> }
) => {
  try {
    const { name } = await params;

    const role = await getRoleByName(name);

    if (!role) {
      return new NextResponse("Role not found", { status: 404 });
    }

    return new NextResponse(JSON.stringify(role), { status: 200 });
  } catch (error) {
    console.error(error);
    return new NextResponse("Failed to get role", { status: 500 });
  }
};
