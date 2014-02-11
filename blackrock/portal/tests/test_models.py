from blackrock.portal.models import Audience, DigitalFormat, Facet
from blackrock.portal.models import Institution, LocationSubtype
from blackrock.portal.models import LocationType, PersonType, PublicationType
from blackrock.portal.models import RegionType, RightsType, Tag, Url
from blackrock.portal.models import DigitalObject, Location, Station
from blackrock.portal.models import Person, Publication, LearningActivity
from blackrock.portal.models import ResearchProject, DataSet, PhotoGalleryItem
from blackrock.portal.models import ForestStory, Region
from django.test import TestCase
from datetime import datetime


class TestPortalModels(TestCase):
    def setUp(self):
        self.audience = Audience(name="audience name")
        self.audience.save()
        self.digital_format_image = DigitalFormat(name="png", id=1866)
        self.digital_format_image.save()
        self.digital_format_video = DigitalFormat(name="mp4", id=1200)
        self.digital_format_video.save()
        self.facet = Facet(name="facet name here",
                           display_name="facet display name",
                           facet="facet here...")
        self.facet.save()
        self.institution = Institution(name="institution name here")
        self.institution.save()
        self.location_subtype = LocationSubtype(name="location subtype name")
        self.location_subtype.save()
        self.location_type = LocationType(name="location type name")
        self.location_type.save()
        self.person_type = PersonType(name="special type of person")
        self.person_type.save()
        self.publication_type = PublicationType(name="publication name")
        self.publication_type.save()
        self.region_type = RegionType(name="region name")
        self.region_type.save()
        self.tag = Tag(name="tag name")
        self.tag.save()
        self.url = Url(
            name="http://www.ccnmtl.columbia.edu",
            display_name="ccnmtl.columbia.edu")
        self.url.save()
        self.digital_object = DigitalObject(
            name="digital object name",
            digital_format=self.digital_format_image)
        self.digital_object.save()
        self.location = Location(
            name="location name here", latitude=6.08, longitude=2.2)
        self.location.save()
        self.station = Station(name="station name",
                               description="this is a station object",
                               access_means="you can walk there!",
                               activation_date=datetime.now(),
                               location=self.location)
        self.station.save()
        self.person = Person(
            full_name="Harold The Flying Sheep",
            first_name="Harold", last_name="Sheep",
            description=(
                "most people have 2 legs, Harold has 4 and can fly with wings"
            ))
        self.person.save()
        self.person_no_first_name = Person(
            full_name="person has no name", last_name="Sheep No. 2")
        self.person_no_first_name.save()
        self.publication_long_name = Publication(
            name=("This is a very very long publication name, "
                  "long as in longer than twenty five (25) characters"))
        self.publication_long_name.save()
        self.publication = Publication(name="Regular Publication Name")
        self.publication.save()
        self.dataset = DataSet(name="data set",
                               description="This is a data set.",
                               collection_start_date=datetime.now(),
                               location=self.location)
        self.dataset.save()
        self.rights_type = RightsType(name="Rights Type Name")
        self.photo_gallery_item = PhotoGalleryItem(
            title="photo_gallery_item", position=7)
        self.photo_gallery_item.save()
        self.learning_activity = LearningActivity(
            name="Learning Activity Name")
        self.learning_activity.save()
        self.research_project_normal_name = ResearchProject(
            name="This is normal name", start_date=datetime.now())
        self.research_project_normal_name.save()
        self.research_project_long_name = ResearchProject(
            name=("This is a research project with an extrememly "
                  "long name, this name is more like a description "
                  "because the user did not follow the directions "
                  "for entering a propername."),
            start_date=datetime.now())
        self.research_project_long_name.save()
        self.forest_story = ForestStory(name="Name of Forest Story")
        self.forest_story.save()
        self.region = Region(name="Region Name",
                             description="This is some region of blackrock.")
        self.region.save()

    def test_audience_unicode(self):
        self.assertEquals(unicode(self.audience), self.audience.name)

    def test_digital_format_unicode(self):
        self.assertEquals(unicode(self.digital_format_image),
                          self.digital_format_image.name)

    def test_digital_format_is_image(self):
        self.assertTrue(self.digital_format_image.is_image())

    def test_digital_format_is_video(self):
        self.assertTrue(self.digital_format_video.is_video())

    def test_facet_unicode(self):
        self.assertEquals(unicode(self.facet), self.facet.display_name)

    def test_facet_solr_name(self):
        self.assertEquals(self.facet.solr_name(), 'facet_here...')

    def test_institution_name(self):
        self.assertEquals(unicode(self.institution),
                          "institution name here")

    def test_location_subtype(self):
        self.assertEquals(unicode(self.location_subtype),
                          self.location_subtype.name)

    def test_location_type(self):
        self.assertEquals(unicode(self.location_type), self.location_type.name)

    def test_person_type(self):
        self.assertEquals(unicode(self.person_type),
                          self.person_type.name)

    def test_publication_type(self):
        self.assertEquals(unicode(self.publication_type),
                          self.publication_type.name)

    def test_region_type_uni(self):
        self.assertEquals(unicode(self.region_type), self.region_type.name)

    def test_rights_type_uni(self):
        self.assertEquals(unicode(self.rights_type), self.rights_type.name)

    def test_tag_uni(self):
        self.assertEquals(unicode(self.tag), self.tag.name)

    def test_url_uni(self):
        self.assertEquals(unicode(self.url), self.url.name)

    def test_url_doc(self):
        self.assertEquals(self.url.document(), 'www.ccnmtl.columbia.edu')

    def test_digital_obj_uni(self):
        self.assertEquals(
            unicode(self.digital_object), self.digital_object.name)

    def test_location_uni(self):
        self.assertEquals(
            unicode(self.location),
            "%s (%.6f,%.6f)" % (self.location.name,
                                self.location.latitude,
                                self.location.longitude))

    def test_station_related_ex(self):
        # this is not a good test but not entirely sure
        # where it is getting its dataset and research projects from
        self.assertIsNotNone(self.station.related_ex())

    def test_station_research_objects(self):
        self.assertIsNotNone(self.station.research_projects())

    def test_station_datasets(self):
        self.assertIsNotNone(self.station.datasets())

    def test_station_uni(self):
        self.assertEquals(unicode(self.station), self.station.name)

    def test_dataset_unicode(self):
        self.assertEquals(unicode(self.dataset), self.dataset.name)

    def test_regular_publication_uni(self):
        self.assertEquals(unicode(self.publication), self.publication.name)

    def test_long_publication_uni(self):
        self.assertEquals(
            unicode(self.publication_long_name),
            "%s..." % self.publication_long_name.name[0:25])

    def test_dataset_station_is_none(self):
        self.new_none_data_set_location = Location(
            name="New Dataset Location", latitude=6.08, longitude=2.2)
        self.new_none_data_set_location.save()
        self.new_none_dataset = DataSet(
            name="data set",
            description="This is a data set.",
            collection_start_date=datetime.now(),
            location=self.new_none_data_set_location)
        self.new_none_dataset.save()
        self.assertIsNone(self.new_none_dataset.station())

    def test_dataset_station_not_none(self):
        self.data_set_location = Location(
            name="New Dataset Location", latitude=6.08, longitude=2.2)
        self.data_set_location.save()
        self.data_set_station = Station(
            name="New Station",
            description="this is a another station object",
            access_means="you can walk there!",
            activation_date=datetime.now(),
            location=self.location)
        self.data_set_station.save()
        self.new_dataset = DataSet(name="data set",
                                   description="This is a data set.",
                                   collection_start_date=datetime.now(),
                                   location=self.location)
        self.new_dataset.save()
        self.data_set_location.station_set.add(self.data_set_station)
        self.data_set_location.dataset_set.add(self.new_dataset)
        self.data_set_location.save()
        self.assertIsNotNone(self.dataset.station())

    def test_person_unicode(self):
        self.assertEquals(
            unicode(self.person),
            "%s, %s" % (self.person.last_name, self.person.first_name))

    def test_person_name(self):
        self.assertEquals(
            self.person.name(),
            "%s, %s" % (self.person.last_name, self.person.first_name))

    def test_person_name_no_name(self):
        self.assertEquals(
            self.person_no_first_name.name(),
            self.person_no_first_name.last_name)

    def test_person_display_name(self):
        self.assertEquals(
            self.person.display_name(),
            "%s %s" % (self.person.first_name, self.person.last_name))

    def test_photo_gallery_item_uni(self):
        self.assertEquals(
            unicode(self.photo_gallery_item), self.photo_gallery_item.title)

    def test_research_project_regular_name(self):
        self.assertEquals(
            unicode(self.research_project_normal_name),
            self.research_project_normal_name.name)

    def test_research_project_long_name(self):
        self.assertEquals(
            unicode(self.research_project_long_name),
            "%s..." % self.research_project_long_name.name[0:50])

    def test_learning_activity_uni(self):
        self.assertEquals(
            unicode(self.learning_activity),
            self.learning_activity.name)

    def test_forest_story_uni(self):
        self.assertEquals(unicode(self.forest_story), self.forest_story.name)

    def test_station_dataset(self):
        ''' Make sure datasets returns dataset
        - there is currently one associated with the location.'''
        self.assertIsNotNone(self.station.datasets())
        self.assertEquals(len(self.station.datasets()), 1)

    def test_station_research_project(self):
        '''This goes over the datasets returned in the
        previous method and gets their research projects and returns them.'''
        self.dataset.researchproject_set.add(self.research_project_long_name)
        self.dataset.researchproject_set.add(self.research_project_normal_name)
        self.dataset.save()
        self.assertIsNotNone(self.station.research_projects())
        self.assertEquals(len(self.station.research_projects()), 2)

    def test_region_uni(self):
        self.assertEquals(unicode(self.region), self.region.name)

    def test_region_learning_activites(self):
        self.learning_activity_1 = LearningActivity(
            name="Learning Activity 1",
            description="This is a learning activity test.")
        self.learning_activity_2 = LearningActivity(
            name="Learning Activity 2",
            description="This is a learning activity test.")
        self.learning_activity_3 = LearningActivity(
            name="Learning Activity 3",
            description="This is a learning activity test.")
        self.learning_activity_1.save()
        self.learning_activity_2.save()
        self.learning_activity_3.save()
        self.location.learningactivity_set.add(self.learning_activity_1)
        self.location.learningactivity_set.add(self.learning_activity_2)
        self.location.learningactivity_set.add(self.learning_activity_3)
        self.location.region_set.add(self.region)
        self.region.save()
        self.location.save()
        self.assertIsNotNone(self.region.learning_activities())
        self.assertEquals(len(self.region.learning_activities()), 3)

    def test_region_research_projects_sets(self):
        self.research_project_1 = ResearchProject(
            name="Research Project 1",
            description="This is a test research project.",
            start_date=datetime.now())
        self.research_project_2 = ResearchProject(
            name="Research Project 2",
            description="This is a test research project.",
            start_date=datetime.now())
        self.research_project_3 = ResearchProject(
            name="Research Project 3",
            description="This is a test research project.",
            start_date=datetime.now())
        self.research_project_1.save()
        self.research_project_2.save()
        self.research_project_3.save()
        self.location.researchproject_set.add(self.research_project_1)
        self.location.researchproject_set.add(self.research_project_2)
        self.location.researchproject_set.add(self.research_project_3)
        self.location.region_set.add(self.region)
        self.region.save()
        self.location.save()
        self.assertIsNotNone(self.region.research_projects())
        self.assertEquals(len(self.region.research_projects()), 3)

    def test_region_datasets(self):
        self.reg_location = Location(
            name="region test location name", latitude=6.08, longitude=2.2)
        self.reg_location.save()
        self.reg_dataset_1 = DataSet(
            name="region test data set",
            description="This is a data set.",
            collection_start_date=datetime.now(),
            location=self.reg_location)
        self.reg_dataset_1.save()
        self.reg_dataset_2 = DataSet(
            name="another region test data set",
            description="This is a data set.",
            collection_start_date=datetime.now(),
            location=self.reg_location)
        self.reg_dataset_2.save()
        self.reg_region = Region(
            name="Region Name",
            description="This is some region of blackrock.")
        self.reg_region.save()
        self.reg_location.region_set.add(self.reg_region)
        self.reg_location.save()
        self.assertIsNotNone(self.reg_region.datasets())
        self.assertEquals(len(self.reg_region.datasets()), 2)

    def test_research_project_related_ex(self):
        '''Method returns an array of datasets - create new
        datasets to associate with new research project, count how many'''
        self.test_location = Location(
            name="location name here", latitude=6.08, longitude=2.2)
        self.test_location.save()

        self.rp_dataset_1 = DataSet(
            name="dataset test",
            description="This is a data set.",
            collection_start_date=datetime.now(),
            location=self.test_location)
        self.rp_dataset_1.save()
        self.rp_dataset_2 = DataSet(
            name="dataset test",
            description="This is a data set.",
            collection_start_date=datetime.now(),
            location=self.test_location)
        self.rp_dataset_2.save()

        self.research_project_dataset = ResearchProject(
            name="dataset test", start_date=datetime.now())
        self.research_project_dataset.save()

        self.rp_dataset_1.researchproject_set.add(
            self.research_project_dataset)
        self.rp_dataset_1.save()
        self.rp_dataset_2.researchproject_set.add(
            self.research_project_dataset)
        self.rp_dataset_2.save()

        self.assertEquals(len(self.research_project_dataset.related_ex()), 2)

    def test_learning_activity_related_ex(self):
        '''Returns array of people and datasets'''
        self.test_location = Location(
            name="location name here", latitude=6.08, longitude=2.2)
        self.test_location.save()

        self.la_dataset_1 = DataSet(
            name="dataset test",
            description="This is a data set.",
            collection_start_date=datetime.now(),
            location=self.test_location)
        self.la_dataset_1.save()
        self.la_dataset_2 = DataSet(
            name="dataset test",
            description="This is a data set.",
            collection_start_date=datetime.now(),
            location=self.test_location)
        self.la_dataset_2.save()

        self.learning_activity_dataset = LearningActivity(
            name="dataset test")
        self.learning_activity_dataset.save()

        self.la_dataset_1.learningactivity_set.add(
            self.learning_activity_dataset)
        self.la_dataset_1.save()
        self.la_dataset_2.learningactivity_set.add(
            self.learning_activity_dataset)
        self.la_dataset_2.save()
        self.assertEquals(len(self.learning_activity_dataset.related_ex()), 2)

    def test_forest_story_related_ex(self):
        '''Returns array of people and datasets'''
        self.test_location = Location(
            name="location name here", latitude=6.08, longitude=2.2)
        self.test_location.save()

        self.fs_dataset_1 = DataSet(
            name="dataset test",
            description="This is a data set.",
            collection_start_date=datetime.now(),
            location=self.test_location)
        self.fs_dataset_1.save()
        self.fs_dataset_2 = DataSet(
            name="dataset test",
            description="This is a data set.",
            collection_start_date=datetime.now(),
            location=self.test_location)
        self.fs_dataset_2.save()

        self.forest_story_dataset = ForestStory(name="dataset test")
        self.forest_story_dataset.save()

        self.fs_dataset_1.foreststory_set.add(self.forest_story_dataset)
        self.fs_dataset_1.save()
        self.fs_dataset_2.foreststory_set.add(self.forest_story_dataset)
        self.fs_dataset_2.save()
        self.assertEquals(len(self.forest_story_dataset.related_ex()), 2)