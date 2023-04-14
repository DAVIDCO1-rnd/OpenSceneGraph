//page 47 (70 of 412)
#include <osgDB/ReadFile>
#include <osgViewer/Viewer>

int main(int argc, char** argv)
{
	osg::ref_ptr<osg::Node> root = osgDB::readNodeFile("C:/Users/David Cohn/Documents/Github/OGL_folders/OpenSceneGraph/OpenSceneGraph-Data-3.4.0/cessna.osg");	
	osgViewer::Viewer viewer;
	if (root.valid() == true)
	{
		osg::Node* rootPointer = root.get();
		viewer.setSceneData(rootPointer);
	}
	return viewer.run();
}