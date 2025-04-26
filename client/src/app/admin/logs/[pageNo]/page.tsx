import React from "react";
import AdminLogs from "@components/admin/AdminLogs";
import { auth } from "@/src/auth";
import Warning from "@components/Warning";
import { getTotalLogsPagesAction } from "@/src/app/actions/logs";
import Pagination from "@components/admin/Pagination";
import { Permissions } from "@/src/app/lib/enums";

const page = async ({ params }: { params: Promise<{ pageNo: number }> }) => {
  const { pageNo } = await params;

  const currentPage = Number(pageNo);

  const session = await auth();

  if (!session?.user.roleId.permissions?.includes(Permissions.Logs)) {
    return <Warning />;
  }

  const itemsLimit = 18;

  const totalPages = await getTotalLogsPagesAction(itemsLimit);

  return (
    <>
      <div className="md:h-[59rem]">
        <AdminLogs page={currentPage} itemsPerPage={itemsLimit} />
      </div>
      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        url="/admin/logs/"
      />
    </>
  );
};

export default page;
