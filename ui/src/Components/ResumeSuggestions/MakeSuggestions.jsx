import React from 'react';
import { Button, Form, Spin, Input, message, Modal, Select } from 'antd';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import config from '../../config';
import { useEffect, useState } from 'react';


export function MakeSuggestions({isOpen, onClose, updateSuggestions}) {
    const [form] = Form.useForm();
    const { state } = useLocation();
	const [loadingDownload, setLoadingDownload] = useState(false);
    const [files, setFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState("");

    useEffect(() => {
        updateFiles();
    }, []);

    const updateFiles = () => {
        setLoadingDownload(true);
        axios
        .get(`${config.base_url}/view_files?email=` + state.email)
			.then(({ data }) => setFiles(data.files))
			.catch((err) => console.log(err))
            .finally(() => setLoadingDownload(false));
    };

    const closeForm = () => {
        form.resetFields();
        onClose();
    }

    const updateSelectedFile = (val) => {
        setSelectedFile(val);
    }

    const sendRequest = (vals) => {
        setLoadingDownload(true);
        axios
        .post(`${config.base_url}/resume_suggest`, { ...vals, email: state.email, file: selectedFile })
        .then(({ data }) => {
            message.success(data.message);
            updateSuggestions(data.suggestions);
            closeForm();
        })
        .catch((err) => message.error(err.response.data?.error))
        .finally(() => setLoadingDownload(false));
    }

    return (
        <Modal
            title="Make Cover Letter"
            open={isOpen}
            onCancel={closeForm}
            width={700}
            centered
            footer={[
                <Button onClick={closeForm} key="cancel" id="cancel">
                    Cancel
                </Button>,
                <Button type="primary" 
                disabled={loadingDownload}
                onClick={() => {form.submit(); setLoadingDownload(true)}} id="add-submit" key="ok">
                    Submit
                </Button>,
            ]}
        >
            {loadingDownload && <Spin></Spin>}
            <p>Choose Resume:</p>
            <Select
            placeholder="Select an option"
            onChange={updateSelectedFile}
            disabled={files.length === 0 || loadingDownload}
            >
            {files.map((file) => (
                <Option key={file._id} value={file.filename}>
                {file.filename.split('--;--')[1]}
                </Option>
            ))}
            </Select>

            <Form form={form} layout="vertical" requiredMark={false} onFinish={sendRequest}>
                <Form.Item
                    label="Context"
                    name="context">
                    <Input placeholder="Input Additional Context" disabled={loadingDownload} />
                </Form.Item>
                <Form.Item
                    label="Job Description"
                    name="job_desc"
                    rules={[
                        {
                            required: true,
                            message: 'Please input job description to tailor the Cover Letter!',
                        },
                    ]}
                >
                    <Input.TextArea placeholder="Job Description" disabled={loadingDownload} />
                </Form.Item>
            </Form>
        </Modal>
    );
}