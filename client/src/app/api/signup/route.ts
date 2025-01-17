import { NextRequest, NextResponse } from "next/server";
import { hash } from "bcryptjs";
import { createUser, getRoleByName, getUser } from "../../lib/data";
import { IRole } from "../../lib/models";

export const POST = async (req: NextRequest) => {
  try {
    const body = await req.json();
    const { username, password, role } = body;

    if (!username || !password || !role) {
      return new NextResponse("Missing fields", { status: 400 });
    }

    if (await getUser(username)) {
      return new NextResponse("User already exists", { status: 409 });
    }
  
    const roleId: IRole = await getRoleByName(role);

    if (!roleId) {
      return new NextResponse("Role not found", { status: 404 });
    }

    const hashedPassword = await hash(password, 10);

    const user = await createUser(username, hashedPassword, roleId._id);

    return new NextResponse(JSON.stringify(user), { status: 201 });
  } catch (error) {
    console.error(error);
    return new NextResponse("Failed to create user", { status: 500 });
  }
};
