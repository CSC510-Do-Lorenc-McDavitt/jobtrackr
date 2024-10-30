import React, { useEffect, useState } from 'react';
import { Button, Card, Tag, Typography } from 'antd';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
<<<<<<< HEAD
import { DownloadOutlined } from '@ant-design/icons';
import { PlusOutlined } from '@ant-design/icons';
import config from '../../config';
import './ResumeSuggestions.scss'
import { MakeSuggestions } from './MakeSuggestions';

export function ResumeSuggestions() {
    const [resumeSuggestion, setResumeSuggestion] = useState("");
    const [makeResumeSuggestionOpen, setResumeSuggestionOpen] = useState(false);
	const { state } = useLocation();

	useEffect(() => {
		updateResumeSuggestion("");
	}, []);
	const updateResumeSuggestion = (content) => {
		setResumeSuggestion(content);
	}
    const toggleMakeResumeSuggestion = () => setResumeSuggestionOpen(!makeResumeSuggestionOpen);
	const getSuggestion = () => {
		const url = window.URL.createObjectURL(new Blob([resumeSuggestion], {type: 'text/plain'}));
			const link = document.createElement('a');
			link.href = url;
			link.setAttribute('download', "resume_suggestions.txt");
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
	}
	return (
        
		<div className="ResumeSuggestion">
			<div className="SubHeader">
				<div className="flex" />
				<div className="SubHeader">
					<div className="flex" />
					<Button
						id="generate-cv"
						type="primary"
						size="large"
						icon={<PlusOutlined />}
                        onClick={toggleMakeResumeSuggestion}
					>
						Generate Resume Suggestions
					</Button>
                    <MakeSuggestions
                        isOpen={makeResumeSuggestionOpen}
                        onClose={toggleMakeResumeSuggestion}
                        updateResumeSuggestion={updateResumeSuggestion}
                    />
				</div>
            </div>

             <div className="ResumeSuggest">
                 <Card className="ResumeCard" key={1} title={"Resume Suggestions"}>
                     {resumeSuggestion}
		 								{resumeSuggestion.length > 0 && 
		 								<>
		 								<br /> 
		 								<Button
		 									id="download"
		 									type="primary"
		 									size="large"
		 									icon={<DownloadOutlined />}
		 									onClick={getSuggestion}
		 								>
		 									Download
		 								</Button>
		 								</>}
                 </Card>
		 	</div>
       
		    </div>
        
    );
    
=======
import config from '../../config';
import './ResumeSuggestions.scss'

export function ResumeSuggestions() {

    
    return (

    );
>>>>>>> 2589deb8ef389a5138f28519da6fe658e67e3437
}