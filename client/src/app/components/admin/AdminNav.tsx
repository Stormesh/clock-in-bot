import React from 'react'
import AdminNavLink from './AdminNavLink'

const AdminNav = () => {
  return (
    <nav className='flex bg-purple-300/35'>
        <AdminNavLink href='/admin/users' text='Manage Users' />
        <AdminNavLink href='/admin/logs' text='Logs' />
    </nav>
  )
}

export default AdminNav