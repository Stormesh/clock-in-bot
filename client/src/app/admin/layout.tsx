import { auth } from "@/src/auth";
import Warning from "@components/Warning";
import AdminNav from "@components/admin/AdminNav";
import Link from "next/link";

export default async function AdminLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const session = await auth();

  // Check if user is not an admin
  if (session?.user.roleId.priority && session.user.roleId.priority >= 2) {
    return (
      <Warning />
    );
  }

  return (
    <div className="flex items-center justify-center">
      <main className="bg-black/25 w-screen border-2 border-table-border h-screen overflow-y-scroll">
        <AdminNav />
        {children}
        <div className="flex justify-center">
        <Link className="mt-2" href="/">
          <button className="bg-green-700 hover:bg-green-500 hover:scale-105 transition-all p-2 font-bold rounded-lg text-white cursor-pointer">
            Go back
          </button>
        </Link>
        </div>
      </main>
    </div>
  );
}
