import React from 'react'
import AdminLogs from '../../components/admin/AdminLogs'
import { auth } from '@/src/auth'
import Warning from '../../components/Warning';

const page = async () => {
  const session = await auth();

  if (!session?.user.roleId.permissions?.includes("view-logs")) {
    return (
      <Warning />
    );
  }

  return (
    <AdminLogs />
  )
}

export default page