from app.hospital.models import Ward, RoomClass, WardRoomClassAssignment, WardRoom, Bed, Admission
from app.patients.models import Patient
from app.auth.models import db
from sqlalchemy import and_, or_


class PatientPlacementService:
    @staticmethod
    def get_optimal_ward(patient, required_care_level=None, required_specialty=None):
        """
        Get the optimal ward for a patient based on their needs and ward preferences.
        
        Args:
            patient (Patient): The patient to be placed
            required_care_level (str): Required care level for the patient
            required_specialty (str): Required specialty for the patient
            
        Returns:
            Ward: The optimal ward for the patient, or None if no suitable ward is found
        """
        # Get all active wards
        wards = Ward.query.filter_by(is_active=True).all()
        
        # If no wards are available, return None
        if not wards:
            return None
            
        # Get ward-room class assignments
        assignments = WardRoomClassAssignment.query.filter_by(is_active=True).all()
        
        # Create a mapping of ward_id to assignments
        ward_assignments = {}
        for assignment in assignments:
            if assignment.ward_id not in ward_assignments:
                ward_assignments[assignment.ward_id] = []
            ward_assignments[assignment.ward_id].append(assignment)
            
        # Score each ward based on preferences and availability
        ward_scores = []
        for ward in wards:
            score = PatientPlacementService._calculate_ward_score(
                ward, patient, required_care_level, required_specialty, ward_assignments
            )
            if score > 0:  # Only consider wards with a positive score
                ward_scores.append((ward, score))
                
        # Sort wards by score in descending order
        ward_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return the ward with the highest score, or None if no suitable ward is found
        return ward_scores[0][0] if ward_scores else None
    
    @staticmethod
    def _calculate_ward_score(ward, patient, required_care_level, required_specialty, ward_assignments):
        """
        Calculate a score for a ward based on various factors.
        
        Args:
            ward (Ward): The ward to score
            patient (Patient): The patient to be placed
            required_care_level (str): Required care level for the patient
            required_specialty (str): Required specialty for the patient
            ward_assignments (dict): Mapping of ward_id to assignments
            
        Returns:
            int: The score for the ward
        """
        score = 0
        
        # Check if the ward has a preferred room class
        if ward.preferred_room_class_id:
            preferred_room_class = RoomClass.query.get(ward.preferred_room_class_id)
            if preferred_room_class:
                # Add points if the preferred room class matches requirements
                if required_care_level and preferred_room_class.care_level == required_care_level:
                    score += 10
                if required_specialty and preferred_room_class.specialty == required_specialty:
                    score += 10
                    
                # Check if there are available beds in the preferred room class
                available_beds = Bed.query.join(WardRoom).filter(
                    and_(
                        Bed.is_occupied == False,
                        Bed.is_active == True,
                        WardRoom.ward_id == ward.id,
                        WardRoom.room_class_id == preferred_room_class.id
                    )
                ).count()
                
                if available_beds > 0:
                    score += 5  # Add points for available beds
                    
        # Check ward-room class assignments
        if ward.id in ward_assignments:
            for assignment in ward_assignments[ward.id]:
                room_class = RoomClass.query.get(assignment.room_class_id)
                if room_class:
                    # Add points based on assignment priority
                    score += assignment.priority or 0
                    
                    # Add points if the room class matches requirements
                    if required_care_level and room_class.care_level == required_care_level:
                        score += 5
                    if required_specialty and room_class.specialty == required_specialty:
                        score += 5
                        
                    # Check capacity
                    if assignment.min_capacity and assignment.min_capacity <= available_beds:
                        score += 2
                    if assignment.max_capacity and assignment.max_capacity >= available_beds:
                        score += 2
                        
        # Check overall bed availability in the ward
        available_beds = Bed.query.join(WardRoom).filter(
            and_(
                Bed.is_occupied == False,
                Bed.is_active == True,
                WardRoom.ward_id == ward.id
            )
        ).count()
        
        if available_beds > 0:
            score += 3  # Add points for overall availability
            
        return score
    
    @staticmethod
    def get_optimal_bed(patient, ward, required_care_level=None, required_specialty=None):
        """
        Get the optimal bed for a patient in a specific ward.
        
        Args:
            patient (Patient): The patient to be placed
            ward (Ward): The ward to search for beds
            required_care_level (str): Required care level for the patient
            required_specialty (str): Required specialty for the patient
            
        Returns:
            Bed: The optimal bed for the patient, or None if no suitable bed is found
        """
        # Get all available beds in the ward
        available_beds = Bed.query.join(WardRoom).filter(
            and_(
                Bed.is_occupied == False,
                Bed.is_active == True,
                WardRoom.ward_id == ward.id
            )
        ).all()
        
        # If no beds are available, return None
        if not available_beds:
            return None
            
        # Score each bed based on room class preferences
        bed_scores = []
        for bed in available_beds:
            score = PatientPlacementService._calculate_bed_score(
                bed, patient, required_care_level, required_specialty
            )
            bed_scores.append((bed, score))
            
        # Sort beds by score in descending order
        bed_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return the bed with the highest score
        return bed_scores[0][0] if bed_scores else None
    
    @staticmethod
    def _calculate_bed_score(bed, patient, required_care_level, required_specialty):
        """
        Calculate a score for a bed based on various factors.
        
        Args:
            bed (Bed): The bed to score
            patient (Patient): The patient to be placed
            required_care_level (str): Required care level for the patient
            required_specialty (str): Required specialty for the patient
            
        Returns:
            int: The score for the bed
        """
        score = 0
        
        # Get the room class for this bed
        ward_room = WardRoom.query.filter_by(id=bed.ward_room_id).first()
        if not ward_room:
            return score
            
        room_class = RoomClass.query.get(ward_room.room_class_id)
        if not room_class:
            return score
            
        # Add points if the room class matches requirements
        if required_care_level and room_class.care_level == required_care_level:
            score += 10
        if required_specialty and room_class.specialty == required_specialty:
            score += 10
            
        # Add points if this is the ward's preferred room class
        ward = Ward.query.get(ward_room.ward_id)
        if ward and ward.preferred_room_class_id == room_class.id:
            score += 5
            
        return score
    
    @staticmethod
    def place_patient(patient, required_care_level=None, required_specialty=None):
        """
        Place a patient in the optimal ward and bed.
        
        Args:
            patient (Patient): The patient to be placed
            required_care_level (str): Required care level for the patient
            required_specialty (str): Required specialty for the patient
            
        Returns:
            tuple: (ward, bed) or (None, None) if placement is not possible
        """
        # Get the optimal ward
        ward = PatientPlacementService.get_optimal_ward(
            patient, required_care_level, required_specialty
        )
        
        if not ward:
            return (None, None)
            
        # Get the optimal bed in the ward
        bed = PatientPlacementService.get_optimal_bed(
            patient, ward, required_care_level, required_specialty
        )
        
        if not bed:
            return (None, None)
            
        return (ward, bed)