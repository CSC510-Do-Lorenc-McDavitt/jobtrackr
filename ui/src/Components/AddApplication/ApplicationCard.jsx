import React, { useEffect, useState } from 'react';
import { Button, Card, Tag, Typography } from 'antd';
import { EditFilled } from "@ant-design/icons";

function ApplicationCard({application, modalFunc}) {
    

    return (
        <Card
            
            title={application.companyName}
            extra={
                <Button
                    type="text"
                    icon={<EditFilled />}
                    onClick={() => modalFunc(application)}
                    id={application.jobId + 'edit'}
                />
            }
            
            className="Job"
            bordered={false}
            actions={
                ['rejected', 'accepted'].includes(
                    application.status
                ) && [
                    application.status === 'accepted' ? (
                        <Tag color="#87d068">Accepted</Tag>
                    ) : (
                        application.status === 'rejected' && (
                            <Tag color="#f50">Rejected</Tag>
                        )
                    ),
                ]
            }
        >
            ID: {application.jobId}
            <br />
            Title: {application.jobTitle}
            <br />
            {'URL: '}
            <a href={'//' + application.url} target={'_blank'}>
                {application.url}
            </a>
            <br />
            Notes: {application.description}
        </Card>
    );
};
export default ApplicationCard;