import { deleteUserById, updateUserById } from "@/src/app/lib/data";
import { NextRequest, NextResponse } from "next/server";

export const PUT = async (
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) => {
  try {
    const { id } = await params;
    const body = await req.json();
    console.log(body);

    const user = await updateUserById(id, body);

    return new NextResponse(JSON.stringify(user), { status: 200 });
  } catch (error) {
    console.error("Error updating user:", error);
    return new NextResponse("Failed to update user", { status: 500 });
  }
};

export const DELETE = async (
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) => {
  try {
    const { id } = await params;

    await deleteUserById(id);

    return new NextResponse("Successfully deleted user", { status: 204 });
  } catch (error) {
    console.error("Error deleting user:", error);
    return new NextResponse("Failed to delete user", { status: 500 });
  }
};
