import { Button, Card, Form, Input, Typography } from 'antd';
import React from 'react';
import { Link } from 'react-router-dom';

import './RegisterPage.scss';

export default function RegisterPage() {
	const onFinish = (values) => {
		console.log(values);
	};

	return (
		<div className="RegisterPage">
			<Card bordered={false} title="Register">
				<Form
					initialValues={{ remember: true }}
					onFinish={onFinish}
					autoComplete="off"
					layout="vertical"
					requiredMark={false}
				>
					<Form.Item
						label="First Name"
						name="fname"
						rules={[
							{
								required: true,
								message: 'Please input your first name!',
							},
						]}
					>
						<Input />
					</Form.Item>
					<Form.Item
						label="Last Name"
						name="lname"
						rules={[
							{
								required: true,
								message: 'Please input your last name!',
							},
						]}
					>
						<Input />
					</Form.Item>
					<Form.Item
						label="Email"
						name="email"
						rules={[
							{
								required: true,
								message: 'Please input your email address!',
							},
							{
								type: 'email',
								message: 'The input is not valid E-mail!',
							},
						]}
					>
						<Input />
					</Form.Item>
					<Form.Item
						label="Password"
						name="password"
						rules={[
							{
								required: true,
								message: 'Please input your password!',
							},
						]}
						hasFeedback
					>
						<Input.Password />
					</Form.Item>
					<Form.Item
						label="Confirm Password"
						name="confirmPassword"
						dependencies={['password']}
						hasFeedback
						rules={[
							{
								required: true,
								message: 'Please confirm your password!',
							},
							({ getFieldValue }) => ({
								validator(_, value) {
									if (
										!value ||
										getFieldValue('password') === value
									) {
										return Promise.resolve();
									}
									return Promise.reject(
										new Error(
											'The two passwords that you entered do not match!'
										)
									);
								},
							}),
						]}
					>
						<Input.Password />
					</Form.Item>
					<Form.Item wrapperCol={{ span: 24 }}>
						<Button type="primary" htmlType="submit" block>
							Sign Up!
						</Button>
					</Form.Item>
				</Form>
				<Typography>
					Already have an account? <Link to="/login">Click here</Link>{' '}
					to login.
				</Typography>
			</Card>
		</div>
	);
}