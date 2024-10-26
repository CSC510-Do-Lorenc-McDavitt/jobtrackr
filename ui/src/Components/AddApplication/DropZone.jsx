import React, { useRef } from 'react';
import { useDrop } from 'react-dnd';
import EditApplication from './EditApplication';
import axios from 'axios';
import { useState } from 'react';


const DropZone = ({ title, children }) => {
  const dropRef = useRef(null);
  const [applications, updateApplications] = useState([])
  const [editApplication, setEditApplication] = useState(false);
  
  function onDrop(item) {
    axios.post(`${config.base_url}/modify_application`, {
        ...values,
        _id: item._id,
        status: title,
        email,
    })
    .then(({ data }) => {
        message.success(data.message);
        updateApplications();
    })
    .catch((err) => message.error(err.response.data?.error))
    .finally(() => {
        loading();
        closeForm();
    });
  }
  
  const [{ isOver }, drop] = useDrop({
    accept: 'Card', // Specify the type of items you can drop here
    drop: (item) => onDrop(item), // Function to handle the drop
    collect: (monitor) => ({
      isOver: monitor.isOver(), // Whether an item is hovering over the drop zone
    }),
  });

  return (
    applications.map(
        (application, index) =>
             (
                <Card
                    key={title + index}
                    title={application.companyName}
                    extra={
                        <Button
                            type="text"
                            icon={<EditFilled />}
                            onClick={() => setEditApplication(application)}
                            id={application.jobId + 'edit'}
                        />
                    }
                    draggable={true}
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
            )
    )
  );
};

export default DropZone;