import React from 'react'
import ReportNavbarPlayerSelect from './ReportNavbarPlayerSelect'
import ReportNavbarPullSelect from './ReportNavbarPullSelect'


export default function ReportNavbar() {
    return (
        <div className="ml-auto">
            <div className="d-flex gap-1">
                <ReportNavbarPullSelect />
                <ReportNavbarPlayerSelect />
            </div>
        </div>
    )
}
