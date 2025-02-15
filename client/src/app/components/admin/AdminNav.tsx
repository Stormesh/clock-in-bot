import React from 'react'
import AdminNavLink from './AdminNavLink'

const AdminNav = () => {
  return (
    <nav className='fixed w-full md:static flex bg-table-border'>
        <AdminNavLink href='/admin/users' text='Manage Users' />
        <AdminNavLink href='/admin/logs/1' activePath='/admin/logs' text='Logs' />
    </nav>
  )
}

export default AdminNav