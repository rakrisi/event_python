from firebase_config import firebase_db
from firebase_admin import firestore
from datetime import datetime
from typing import List, Dict, Optional

class EventService:
    def __init__(self):
        self.db = firebase_db.get_db()
        self.events_collection = self.db.collection('events')
        self.registrations_collection = self.db.collection('registrations')
        self.feedback_collection = self.db.collection('feedback')
    
    # Event operations
    def create_event(self, title: str, description: str, date: str) -> str:
        """Create a new event and return its ID"""
        event_data = {
            'title': title,
            'description': description,
            'date': date,
            'created_at': datetime.utcnow()
        }
        doc_ref = self.events_collection.add(event_data)
        return doc_ref[1].id
    
    def get_all_events(self) -> List[Dict]:
        """Get all events ordered by date descending"""
        events = []
        docs = self.events_collection.order_by('date', direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            event_data = doc.to_dict()
            event_data['id'] = doc.id
            events.append(event_data)
        return events
    
    def get_event_by_id(self, event_id: str) -> Optional[Dict]:
        """Get a specific event by ID"""
        doc = self.events_collection.document(event_id).get()
        if doc.exists:
            event_data = doc.to_dict()
            event_data['id'] = doc.id
            return event_data
        return None
    
    # Registration operations
    def create_registration(self, event_id: str, name: str, email: str) -> str:
        """Create a new registration and return its ID"""
        registration_data = {
            'event_id': event_id,
            'name': name,
            'email': email,
            'checked_in': False,
            'feedback_given': False,
            'created_at': datetime.utcnow()
        }
        doc_ref = self.registrations_collection.add(registration_data)
        return doc_ref[1].id
    
    def get_registration_by_id(self, reg_id: str) -> Optional[Dict]:
        """Get a specific registration by ID"""
        doc = self.registrations_collection.document(reg_id).get()
        if doc.exists:
            reg_data = doc.to_dict()
            reg_data['id'] = doc.id
            return reg_data
        return None
    
    def get_registrations_by_event(self, event_id: str) -> List[Dict]:
        """Get all registrations for a specific event"""
        registrations = []
        docs = self.registrations_collection.where('event_id', '==', event_id).stream()
        for doc in docs:
            reg_data = doc.to_dict()
            reg_data['id'] = doc.id
            registrations.append(reg_data)
        return registrations
    
    def get_registrations_by_email(self, email: str) -> List[Dict]:
        """Get all registrations for a specific email with event details"""
        registrations = []
        docs = self.registrations_collection.where('email', '==', email).stream()
        for doc in docs:
            reg_data = doc.to_dict()
            reg_data['id'] = doc.id
            
            # Get event details
            event = self.get_event_by_id(reg_data['event_id'])
            if event:
                reg_data['event_title'] = event['title']
                reg_data['event_description'] = event['description']
                reg_data['event_date'] = event['date']
            
            registrations.append(reg_data)
        return registrations
    
    def update_checkin_status(self, reg_id: str, checked_in: bool = True):
        """Update check-in status of a registration"""
        self.registrations_collection.document(reg_id).update({'checked_in': checked_in})
    
    def update_feedback_status(self, reg_id: str, feedback_given: bool = True):
        """Update feedback status of a registration"""
        self.registrations_collection.document(reg_id).update({'feedback_given': feedback_given})
    
    # Feedback operations
    def create_feedback(self, registration_id: str, rating: int, comment: str) -> str:
        """Create feedback and return its ID"""
        feedback_data = {
            'registration_id': registration_id,
            'rating': rating,
            'comment': comment,
            'created_at': datetime.utcnow()
        }
        doc_ref = self.feedback_collection.add(feedback_data)
        return doc_ref[1].id
    
    def get_feedback_by_event(self, event_id: str) -> List[Dict]:
        """Get all feedback for a specific event with user details"""
        feedback_list = []
        
        # Get all registrations for the event
        registrations = self.get_registrations_by_event(event_id)
        reg_ids = [reg['id'] for reg in registrations]
        
        # Get feedback for these registrations
        for reg_id in reg_ids:
            feedback_docs = self.feedback_collection.where('registration_id', '==', reg_id).stream()
            for doc in feedback_docs:
                feedback_data = doc.to_dict()
                feedback_data['id'] = doc.id
                
                # Add registration details
                registration = next((reg for reg in registrations if reg['id'] == reg_id), None)
                if registration:
                    feedback_data['name'] = registration['name']
                    feedback_data['email'] = registration['email']
                    feedback_data['reg_id'] = reg_id
                
                feedback_list.append(feedback_data)
        
        return feedback_list
    
    def get_event_statistics(self, event_id: str) -> Dict:
        """Get statistics for a specific event"""
        registrations = self.get_registrations_by_event(event_id)
        
        total_registrations = len(registrations)
        checked_in_count = sum(1 for reg in registrations if reg.get('checked_in', False))
        feedback_count = sum(1 for reg in registrations if reg.get('feedback_given', False))
        
        return {
            'total_registrations': total_registrations,
            'checked_in_count': checked_in_count,
            'feedback_count': feedback_count
        }
    
    def get_rating_statistics(self, event_id: str) -> List[Dict]:
        """Get rating distribution for a specific event"""
        feedback_list = self.get_feedback_by_event(event_id)
        
        # Count ratings
        rating_counts = {}
        for feedback in feedback_list:
            rating = feedback.get('rating', 0)
            rating_counts[rating] = rating_counts.get(rating, 0) + 1
        
        # Convert to list format
        rating_stats = []
        for rating in sorted(rating_counts.keys()):
            rating_stats.append({
                'rating': rating,
                'count': rating_counts[rating]
            })
        
        return rating_stats

# Global service instance
event_service = EventService()
