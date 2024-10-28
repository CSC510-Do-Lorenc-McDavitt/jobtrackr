import React, { useEffect, useState } from 'react';
import { Button, Card, Tag, Typography } from 'antd';
import { EditFilled, PlusOutlined } from '@ant-design/icons';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import { DndProvider } from  "react-dnd";
import  Draggable from 'react-draggable';
import { HTML5Backend } from 'react-dnd-html5-backend'
import config from '../../config';
import AddApplication from '../AddApplication/AddApplication';
import EditApplication from '../AddApplication/EditApplication';
import DropZone from '../AddApplication/DropZone';
import './LandingPage.scss';
import ApplicationCard from '../AddApplication/ApplicationCard';

const columns = {
	applied: 'Applied',
	inReview: 'In Review',
	interview: 'Interview',
	decision: 'Decision'
};

export default function LandingPage() {
	const [applications, setApplications] = useState([]);
	const [applied, setApplied] = useState([]);
	const [inReview, setInReview] = useState([]);
	const [interview, setInterview] = useState([]);
	const [decision, setDecision] = useState([]);
	const [loading, setLoading] = useState(true);
	const [addApplicationOpen, setAddApplicationOpen] = useState(false);
	const [editApplication, setEditApplication] = useState(false);
	const { state } = useLocation();

	useEffect(() => {
		updateApplications();
	}, []);

	const updateApplications = () => {
		axios
			.get(`${config.base_url}/view_applications?email=` + state.email)
			.then(({ data }) => {
				for (let i = 0; i < data.applications.length; i++) {
					if (data.applications[i].status === "applied") {
						setApplied([...applied, data.applications[i]])
					}
					else if (data.applications[i].status === "inReview") {
						setInReview([...inReview, data.applications[i]])
					}
					else if (data.applications[i].status === "interview") {
						setInterview([...interview, data.applications[i]])
					}
					else if (data.applications[i].status === "decision") {
						setDecision([...decision, data.applications[i]])
					}
				}
				
			})
			.catch((err) => console.log(err))
			.finally(() => setLoading(false));
	};

	const toggleAddApplication = () => setAddApplicationOpen(!addApplicationOpen);

	return (
		<div className="LandingPage">
			<div className="SubHeader">
				<div className="flex" />
				<Button
					id="add-application"
					type="primary"
					size="large"
					icon={<PlusOutlined />}
					onClick={toggleAddApplication}
				>
					Add Application
				</Button>
				<AddApplication
					isOpen={addApplicationOpen}
					onClose={toggleAddApplication}
					updateApplications={updateApplications}
				/>
			</div>

			<div className="MainContent">
				{Object.keys(columns).map((col) => (
					<div className="Status" key={col}>
						<Typography.Title level={5}>
							
							{columns[col]}
							
						</Typography.Title>
						<DndProvider backend={HTML5Backend}>
							<DropZone></DropZone>
						</DndProvider>
						
						{loading ? (
							<>
								<Card loading bordered={false} />
								<Card loading bordered={false} />
								<Card loading bordered={false} />
							</>
						) : (
							<ul>
								{
								applied.map(
									(application, index) =>
										(application.status === col ||
											(col === 'decision' &&
												['rejected', 'accepted'].includes(
													application.status
												))) && (
												
											<ApplicationCard application={application} key={col + index} modalFunc={setEditApplication}></ApplicationCard>
											
										)
								)
							}
							</ul>

								
						)}
						{applications.length === 0 && 'No applications found.'}
					</div>
				))}
			</div>
			{editApplication && (
				<EditApplication
					application={editApplication}
					onClose={() => setEditApplication(false)}
					updateApplications={updateApplications}
					email={state.email}
				/>
			)}
		</div>
	);
}
